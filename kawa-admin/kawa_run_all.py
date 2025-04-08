import os
import subprocess

AGENTS_DIR = "agents"

def run_step(script_name):
    script_path = os.path.join(AGENTS_DIR, script_name)
    print(f"\n--- Lancement de : {script_name} ---")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"[ERREUR] détectée dans {script_name} :\n{result.stderr}")

if __name__ == "__main__":
    print("Démarrage du pipeline KAWA-ADMIN complet")

    run_step("kawa_collect.py")
    run_step("kawa_struct.py")
    run_step("kawa_chunk.py")
    run_step("kawa_embed.py")

    print("\nPipeline termine. Les documents sont prêts pour interrogation RAG.")
