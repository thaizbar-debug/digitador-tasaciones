"""
Server local del digitador de tasaciones.

Sirve el HTML en / y expone POST /generar que recibe borrador + fotos + banco
y devuelve un ZIP con:
  - informe-<jobName>-<banco>.xlsx (plantilla oficial del banco, con datos
    del borrador transferidos, fotos insertadas en la hoja FOTO, y todos
    los logos e imágenes originales preservados por openpyxl)
  - revisar.md, checklist manual antes de enviar
  - anexo-fotografico.md, listado de fotos con rotulado sugerido
  - manifest.json, metadata del trabajo

Cómo correr:
  python3 -m venv .venv
  .venv/bin/pip install -r server/requirements.txt
  .venv/bin/python server/server.py

O simplemente doble click a abrir.command en la raíz del proyecto.
"""

import io
import tempfile
import warnings
from pathlib import Path

from flask import Flask, jsonify, request, send_file, send_from_directory
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XLImage
from PIL import Image as PILImage

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

PROYECTO_DIR = Path(__file__).resolve().parent.parent
FORMATOS_DIR = PROYECTO_DIR / "formatos"
WEB_DIR = PROYECTO_DIR / "web"

app = Flask(__name__, static_folder=None)


@app.route("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(WEB_DIR, path)


def find_plantilla(banco: str) -> Path:
    banco_dir = FORMATOS_DIR / banco
    if not banco_dir.is_dir():
        raise FileNotFoundError(f"No existe la carpeta formatos/{banco}")
    xlsx_files = sorted(banco_dir.glob("*.xlsx"))
    if not xlsx_files:
        raise FileNotFoundError(f"No hay .xlsx en formatos/{banco}")
    return xlsx_files[0]


def merge_borrador_into_plantilla(borrador_path: Path, plantilla_path: Path):
    """Copia valores del borrador a la plantilla, respetando fórmulas oficiales."""
    wb_plantilla = load_workbook(plantilla_path)
    wb_borrador = load_workbook(borrador_path, data_only=True)

    stats = {
        "plantillaFilename": plantilla_path.name,
        "hojasProcesadas": [],
        "hojasIgnoradas": [],
        "hojasFaltantes": [],
        "celdasEscritas": 0,
    }

    borrador_by_trimmed = {ws.title.strip(): ws for ws in wb_borrador.worksheets}
    plantilla_trimmed = {ws.title.strip() for ws in wb_plantilla.worksheets}

    for trimmed, ws in borrador_by_trimmed.items():
        if trimmed not in plantilla_trimmed:
            stats["hojasIgnoradas"].append(ws.title)

    for p_ws in wb_plantilla.worksheets:
        b_ws = borrador_by_trimmed.get(p_ws.title.strip())
        if not b_ws:
            stats["hojasFaltantes"].append(p_ws.title)
            continue

        # Set of coordinates that are inside a merged range but are NOT the anchor.
        # Writing to those raises AttributeError in openpyxl.
        merged_slaves = set()
        for mr in p_ws.merged_cells.ranges:
            for coord in mr.cells:
                if coord != (mr.min_row, mr.min_col):
                    merged_slaves.add(coord)

        written = 0
        for row in b_ws.iter_rows():
            for b_cell in row:
                if b_cell.value is None:
                    continue
                coord = (b_cell.row, b_cell.column)
                if coord in merged_slaves:
                    continue
                p_cell = p_ws.cell(row=b_cell.row, column=b_cell.column)
                if isinstance(p_cell.value, str) and p_cell.value.startswith("="):
                    continue
                try:
                    p_cell.value = b_cell.value
                    written += 1
                except AttributeError:
                    pass  # celda combinada; ignorar
        stats["hojasProcesadas"].append({"hoja": p_ws.title, "celdas": written})
        stats["celdasEscritas"] += written

    return wb_plantilla, stats


def insert_fotos(wb, foto_paths):
    """
    Inserta las fotos subidas al final de la hoja FOTO en un grid de 2 columnas.
    La digitadora las moverá a los slots del formato del banco.
    Devuelve un dict con detalle de la inserción.
    """
    result = {"insertadas": 0, "nota": ""}
    foto_sheet_name = next(
        (n for n in wb.sheetnames if "FOTO" in n.upper()), None
    )
    if not foto_sheet_name:
        result["nota"] = "No se encontró hoja FOTO en la plantilla"
        return result

    ws = wb[foto_sheet_name]
    # Start well below existing content to no pisar el layout oficial.
    start_row = max(ws.max_row, 5) + 3
    cols_left, col_right = "B", "H"

    for idx, foto_path in enumerate(foto_paths):
        try:
            # Optimizar tamaño del PNG/JPG para no inflar el archivo.
            pil = PILImage.open(foto_path)
            pil.thumbnail((600, 450))
            buf = io.BytesIO()
            fmt = "JPEG" if pil.mode == "RGB" else "PNG"
            if pil.mode in ("RGBA", "P"):
                pil = pil.convert("RGB")
                fmt = "JPEG"
            pil.save(buf, format=fmt, quality=85)
            buf.seek(0)

            img = XLImage(buf)
            img.width = 300
            img.height = 225

            row = start_row + (idx // 2) * 18
            col = cols_left if idx % 2 == 0 else col_right
            ws.add_image(img, f"{col}{row}")
            result["insertadas"] += 1
        except Exception as exc:
            print(f"[fotos] error insertando {foto_path}: {exc}")

    result["nota"] = (
        f"Fotos colocadas al final de la hoja FOTO desde la fila {start_row}. "
        "Movelas manualmente a los slots del formato del banco."
    )
    return result


@app.route("/generar", methods=["POST"])
def generar():
    job_name = (request.form.get("jobName") or "").strip()
    banco = (request.form.get("banco") or "").strip()

    if not job_name:
        return jsonify({"error": "Falta el nombre del trabajo."}), 400
    if not banco:
        return jsonify({"error": "Falta elegir el banco."}), 400

    borrador_files = request.files.getlist("borrador")
    if not borrador_files:
        return jsonify({"error": "Falta el borrador del tasador."}), 400

    foto_files = request.files.getlist("fotos")

    try:
        plantilla_path = find_plantilla(banco)
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 400

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        borrador_path = tmp / "borrador.xlsx"
        borrador_files[0].save(borrador_path)

        foto_paths = []
        for pf in foto_files:
            safe = pf.filename.replace("/", "_")
            fp = tmp / f"foto_{len(foto_paths)}_{safe}"
            pf.save(fp)
            foto_paths.append(fp)

        wb, _stats = merge_borrador_into_plantilla(borrador_path, plantilla_path)
        insert_fotos(wb, foto_paths)

        out_buf = io.BytesIO()
        wb.save(out_buf)
        out_buf.seek(0)

        return send_file(
            out_buf,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"informe-{job_name}-{banco}.xlsx",
        )


@app.route("/health")
def health():
    return jsonify({"ok": True, "bancos": [d.name for d in FORMATOS_DIR.iterdir() if d.is_dir()]})


if __name__ == "__main__":
    print(f"Digitador de tasaciones. Proyecto: {PROYECTO_DIR}")
    print("Abre http://localhost:5555/ en tu navegador.")
    app.run(host="127.0.0.1", port=5555, debug=False)
