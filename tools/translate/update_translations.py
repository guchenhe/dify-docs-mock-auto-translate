#!/usr/bin/env python3
"""
Translation Update Script for PR Synchronization

This script handles updating translations when the source English PR is modified.
It re-analyzes the PR changes and updates the corresponding translation files.
"""

import json
import sys
import os
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(__file__))
from sync_and_translate import DocsSynchronizer
from pr_analyzer import PRAnalyzer


async def update_translations(base_sha: str, head_sha: str) -> bool:
    """
    Update translations for a PR that has been modified.
    
    Args:
        base_sha: Base commit SHA
        head_sha: Head commit SHA
        
    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Analyze changes
        print(f"Analyzing PR changes between {base_sha} and {head_sha}")
        analyzer = PRAnalyzer(base_sha, head_sha)
        result = analyzer.categorize_pr()
        
        if result['type'] != 'english':
            print(f"PR type is {result['type']}, not english - skipping")
            return False
        
        # Initialize synchronizer
        api_key = os.environ.get("DIFY_API_KEY")
        if not api_key:
            print("Error: DIFY_API_KEY not set")
            return False
        
        synchronizer = DocsSynchronizer(api_key)
        
        # Get English files that need translation
        file_categories = result['files']
        english_files = file_categories['english']
        
        results = {
            "translated": [],
            "failed": [],
            "skipped": [],
            "updated": True
        }
        
        print(f"Found {len(english_files)} English files to update translations for")
        
        # Translate English files (limit to 10 files for safety)
        for file_path in english_files[:10]:
            print(f"Updating translations for: {file_path}")
            
            if not os.path.exists(file_path):
                print(f"Warning: File {file_path} not found, skipping")
                results["skipped"].append(file_path)
                continue
                
            try:
                for target_lang in ["zh-hans", "ja-jp"]:
                    target_path = file_path.replace("en/", f"{target_lang}/")
                    print(f"  Translating to {target_lang}: {target_path}")
                    
                    success = await synchronizer.translate_file_with_notice(
                        file_path,
                        target_path,
                        target_lang
                    )
                    if success:
                        print(f"  ✅ Successfully translated: {target_path}")
                        results["translated"].append(target_path)
                    else:
                        print(f"  ❌ Failed to translate: {target_path}")
                        results["failed"].append(target_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                results["failed"].append(file_path)
        
        # Handle docs.json structure sync if needed
        docs_changes = result['docs_json_changes']
        if docs_changes['any_docs_json_changes']:
            print("Updating docs.json structure...")
            try:
                sync_log = synchronizer.sync_docs_json_structure()
                print("\n".join(sync_log))
            except Exception as e:
                print(f"Error syncing docs.json structure: {e}")
        
        # Save results
        results_file = "/tmp/update_results.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {results_file}")
        
        # Report summary
        total_translated = len(results["translated"])
        total_failed = len(results["failed"])
        total_skipped = len(results["skipped"])
        
        print(f"\nTranslation Update Summary:")
        print(f"  ✅ Translated: {total_translated} files")
        print(f"  ❌ Failed: {total_failed} files")
        print(f"  ⏭️  Skipped: {total_skipped} files")
        
        return total_failed == 0
        
    except Exception as e:
        print(f"Critical error in update_translations: {e}")
        return False


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 3:
        print("Usage: update_translations.py <base_sha> <head_sha>")
        sys.exit(1)
    
    base_sha = sys.argv[1]
    head_sha = sys.argv[2]
    
    try:
        success = asyncio.run(update_translations(base_sha, head_sha))
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()