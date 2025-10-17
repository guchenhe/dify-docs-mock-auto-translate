import json
import sys
import os
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(__file__))
from sync_and_translate import DocsSynchronizer

async def secure_sync():
    work_dir = sys.argv[1]
    
    # Load sync plan
    with open(f"{work_dir}/sync_plan.json") as f:
        sync_plan = json.load(f)
    
    # Security: Only sync files from the approved list
    files_to_sync = sync_plan.get("files_to_sync", [])
    
    # Validate file paths again
    for file_info in files_to_sync:
        file_path = file_info["path"]

        # Security checks
        if ".." in file_path or file_path.startswith("/"):
            print(f"Security error: Invalid path {file_path}")
            return False

        # Allow en/ files and docs.json
        if not (file_path.startswith("en/") or file_path == "docs.json"):
            print(f"Security error: File outside en/ directory: {file_path}")
            return False
    
    # Initialize synchronizer
    api_key = os.environ.get("DIFY_API_KEY")
    if not api_key:
        print("Error: DIFY_API_KEY not set")
        return False
    
    synchronizer = DocsSynchronizer(api_key)
    
    # Perform limited sync
    results = {
        "translated": [],
        "failed": [],
        "skipped": []
    }
    
    for file_info in files_to_sync[:10]:  # Limit to 10 files
        file_path = file_info["path"]
        print(f"Processing: {file_path}")

        # Skip docs.json - it's handled separately in structure sync
        if file_path == "docs.json":
            results["skipped"].append(f"{file_path} (structure file - handled separately)")
            continue

        # Skip versioned directories (frozen/archived docs)
        if file_path.startswith("versions/"):
            results["skipped"].append(f"{file_path} (versioned - not auto-translated)")
            continue

        try:
            # Only translate if file exists and is safe
            if os.path.exists(f"../../{file_path}"):
                for target_lang in ["cn", "jp"]:
                    target_path = file_path.replace("en/", f"{target_lang}/")
                    success = await synchronizer.translate_file_with_notice(
                        file_path,
                        target_path,
                        target_lang
                    )
                    if success:
                        results["translated"].append(target_path)
                    else:
                        results["failed"].append(target_path)
            else:
                results["skipped"].append(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            results["failed"].append(file_path)
    
    # Handle docs.json structure sync if needed
    if sync_plan.get("structure_changes", {}).get("structure_changed"):
        print("Syncing docs.json structure...")
        try:
            sync_log = synchronizer.sync_docs_json_structure()
            print("\n".join(sync_log))
        except Exception as e:
            print(f"Error syncing structure: {e}")
    
    # Save results
    with open("/tmp/sync_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return len(results["failed"]) == 0

if __name__ == "__main__":
    success = asyncio.run(secure_sync())
    sys.exit(0 if success else 1)
