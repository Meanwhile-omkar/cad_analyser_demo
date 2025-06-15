import streamlit as st
import trimesh
import os
import tempfile
import pandas as pd
from vedo import Mesh, Plotter, show
import uuid

st.set_page_config(page_title="CAD Analyzer", layout="wide")
st.title("🧩 CAD File Analyzer and Viewer")

# File uploader with extended format support
uploaded_file = st.file_uploader(
    "Upload a CAD file (.stl, .obj, .ply, .glb, .gltf, .off, .3mf, .dae, .fbx, .amf)",
    type=['stl', 'obj', 'ply', 'glb', 'gltf', 'off', '3mf', 'dae', 'fbx', 'amf']
)

if uploaded_file is not None:
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        # Load the CAD mesh
        mesh = trimesh.load(tmp_path)
        st.success("✅ CAD file loaded successfully!")

        # Mesh analysis
        info = {
            "📐 Volume": mesh.volume,
            "📏 Surface Area": mesh.area,
            "📦 Bounding Box": mesh.bounds.tolist(),
            "🎯 Center of Mass": mesh.center_mass.tolist(),
            "🔺 Number of Vertices": len(mesh.vertices),
            "🔻 Number of Faces": len(mesh.faces)
        }

        st.subheader("📊 CAD Analytics")
        df = pd.DataFrame([info]).T.rename(columns={0: "Value"})
        st.table(df)

        # Snapshot-based 3D Visualization (in Streamlit)
        st.subheader("🧭 3D Snapshot Preview")

        vmesh = Mesh(mesh)
        vp = Plotter(offscreen=True)
        vp.show(vmesh, axes=1, interactive=False)
        img_path = f"{uuid.uuid4().hex}_snapshot.png"
        vp.screenshot(img_path)
        vp.close()

        st.image(img_path, caption="Rendered CAD Snapshot")

        # Live 3D view (external window)
        if st.button("🔁 Open Interactive 3D Viewer"):
            st.info("A separate interactive window will open outside your browser.")
            show(Mesh(mesh), axes=1)  # opens in external window using vedo

    except Exception as e:
        st.error(f"❌ Error loading CAD file: {str(e)}")
