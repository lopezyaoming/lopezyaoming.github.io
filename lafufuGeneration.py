
import json
import os
import time
import requests
import tempfile
import shutil
from pathlib import Path

class LafufuGenerator:
    def __init__(self):
        self.comfyui_url = "http://127.0.0.1:8188"
        self.workflow_path = "imageGen/Lafufu_wf.json"
        self.prompts_path = "imageGen/labubu_prompts_AVD.json"
        self.assets_path = "assets/lafufu"
        self.temp_dir = tempfile.mkdtemp(prefix="lafufu_")
        
        # Ensure assets directory exists
        os.makedirs(self.assets_path, exist_ok=True)
        
        print(f"Lafufu Generator initialized")
        print(f"ComfyUI URL: {self.comfyui_url}")
        print(f"Temp directory: {self.temp_dir}")
        print(f"Assets directory: {self.assets_path}")
        print(f"Absolute assets path: {os.path.abspath(self.assets_path)}")
        
    def load_workflow(self):
        """Load the base workflow JSON"""
        with open(self.workflow_path, 'r') as f:
            return json.load(f)
    
    def load_prompts(self):
        """Load all prompts from the JSON file"""
        with open(self.prompts_path, 'r') as f:
            return json.load(f)
    
    def create_temp_text_file(self, prompt_content, prompt_key):
        """Create a temporary text file with the prompt content"""
        temp_file_path = os.path.join(self.temp_dir, f"{prompt_key}.txt")
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.write(prompt_content)
        return temp_file_path
    
    def debug_output_settings(self, modified_workflow, prompt_key):
        """Debug helper to show output configuration"""
        if "34" in modified_workflow:
            node34 = modified_workflow["34"]["inputs"]
            print(f"🔧 Output settings for {prompt_key}:")
            print(f"   📁 Output path: {node34.get('output_path')}")
            print(f"   📝 Filename prefix: {node34.get('filename_prefix')}")
            print(f"   🔢 Number padding: {node34.get('filename_number_padding')}")
            print(f"   🔄 Overwrite mode: {node34.get('overwrite_mode')}")
            expected_filename = f"{prompt_key}.png"
            expected_full_path = os.path.join(node34.get('output_path', ''), expected_filename)
            print(f"   📍 Expected file: {expected_full_path}")
        else:
            print(f"⚠️ Node 34 not found in workflow")
    
    def modify_workflow(self, workflow, prompt_key, temp_text_path):
        """Modify the workflow with current prompt settings"""
        # Create a deep copy to avoid modifying the original
        modified_workflow = json.loads(json.dumps(workflow))
        
        # 1. Update image path in node "1"
        if "1" in modified_workflow:
            modified_workflow["1"]["inputs"]["image"] = "assets\\lafufu\\reference_Image.jpg"
        
        # 2. Update text file path in node "35"
        if "35" in modified_workflow:
            modified_workflow["35"]["inputs"]["file_path"] = temp_text_path
            modified_workflow["35"]["inputs"]["dictionary_name"] = f"{prompt_key}.txt"
        
        # 3. Update output filename in node "34"
        if "34" in modified_workflow:
            # Get absolute path to ensure images save to the correct location
            import os
            abs_assets_path = os.path.abspath(self.assets_path)
            modified_workflow["34"]["inputs"]["output_path"] = abs_assets_path
            modified_workflow["34"]["inputs"]["filename_prefix"] = prompt_key
            modified_workflow["34"]["inputs"]["filename_delimiter"] = ""
            modified_workflow["34"]["inputs"]["filename_number_padding"] = 1  # Minimum allowed value
            modified_workflow["34"]["inputs"]["filename_number_start"] = "false"
            modified_workflow["34"]["inputs"]["extension"] = "png"
            modified_workflow["34"]["inputs"]["overwrite_mode"] = "prefix_as_filename"  # Use prefix as filename
        
        return modified_workflow
    
    def check_comfyui_connection(self):
        """Check if ComfyUI is running and accessible"""
        try:
            response = requests.get(f"{self.comfyui_url}/system_stats", timeout=5)
            if response.status_code == 200:
                print("✅ ComfyUI connection successful")
                return True
        except requests.exceptions.RequestException as e:
            print(f"❌ ComfyUI connection failed: {e}")
            return False
        
        return False
    
    def send_workflow_to_comfyui(self, workflow, prompt_key):
        """Send the modified workflow to ComfyUI"""
        try:
            # First, queue the workflow
            response = requests.post(
                f"{self.comfyui_url}/prompt",
                json={"prompt": workflow},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                prompt_id = result.get("prompt_id")
                print(f"✅ Workflow queued for {prompt_key} (ID: {prompt_id})")
                return prompt_id
            else:
                print(f"❌ Failed to queue workflow for {prompt_key}: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending workflow for {prompt_key}: {e}")
            return None
    
    def wait_for_completion(self, prompt_id, timeout=300):
        """Wait for the workflow to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check queue status
                response = requests.get(f"{self.comfyui_url}/queue")
                if response.status_code == 200:
                    queue_data = response.json()
                    
                    # Check if our prompt is still in queue
                    running = queue_data.get("queue_running", [])
                    pending = queue_data.get("queue_pending", [])
                    
                    found_in_queue = False
                    for item in running + pending:
                        if len(item) > 1 and item[1] == prompt_id:
                            found_in_queue = True
                            break
                    
                    if not found_in_queue:
                        print(f"✅ Workflow {prompt_id} completed")
                        return True
                
                time.sleep(2)  # Check every 2 seconds
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Error checking queue status: {e}")
                time.sleep(5)
        
        print(f"⏰ Timeout waiting for workflow {prompt_id}")
        return False
    
    def generate_single_image(self, prompt_key, prompt_content, workflow):
        """Generate a single image for the given prompt"""
        print(f"\n🎨 Processing {prompt_key}...")
        
        # Create temporary text file with the current prompt
        temp_text_path = self.create_temp_text_file(prompt_content, prompt_key)
        print(f"📝 Created temp file: {temp_text_path}")
        
        # Modify workflow for current prompt
        modified_workflow = self.modify_workflow(workflow, prompt_key, temp_text_path)
        
        # Debug output settings (comment out this line to reduce verbosity)
        self.debug_output_settings(modified_workflow, prompt_key)
        
        # Send to ComfyUI
        prompt_id = self.send_workflow_to_comfyui(modified_workflow, prompt_key)
        
        if prompt_id:
            # Wait for completion
            success = self.wait_for_completion(prompt_id)
            if success:
                # With "prefix_as_filename" mode, file should be saved with exact name
                expected_file = os.path.join(self.assets_path, f"{prompt_key}.png")
                
                if os.path.exists(expected_file):
                    print(f"✅ Image saved: {expected_file}")
                    return True
                else:
                    # Check if file exists with any variation in the assets directory
                    import glob
                    search_pattern = os.path.join(self.assets_path, f"{prompt_key}*.png")
                    matching_files = glob.glob(search_pattern)
                    
                    if matching_files:
                        actual_file = matching_files[0]
                        actual_filename = os.path.basename(actual_file)
                        
                        if actual_filename == f"{prompt_key}.png":
                            print(f"✅ Image saved: {actual_file}")
                            return True
                        else:
                            print(f"⚠️ Found file with different name: {actual_filename}")
                            # Try to rename to correct name if needed
                            try:
                                os.rename(actual_file, expected_file)
                                print(f"✅ Renamed to: {expected_file}")
                                return True
                            except Exception as e:
                                print(f"⚠️ Couldn't rename: {e}")
                                print(f"   File saved as: {actual_file}")
                                return True
                    else:
                        print(f"❌ Expected file not found: {expected_file}")
                        print(f"   Check ComfyUI output logs for errors")
                        
                        # Also check if it ended up in ComfyUI's default output directory
                        import glob
                        comfyui_search = os.path.join("C:\\ComfyUI", "**", f"{prompt_key}*.png")
                        comfyui_files = glob.glob(comfyui_search, recursive=True)
                        if comfyui_files:
                            print(f"   🔍 Found in ComfyUI directory: {comfyui_files[0]}")
                            print(f"   💡 Try copying to: {expected_file}")
                        
                        return False
            else:
                print(f"❌ Failed to complete {prompt_key}")
        
        return False
    
    def generate_all_images(self, start_from=None, batch_size=5):
        """Generate all images from the prompts"""
        if not self.check_comfyui_connection():
            print("❌ Cannot connect to ComfyUI. Make sure it's running on http://127.0.0.1:8188")
            return
        
        # Load data
        workflow = self.load_workflow()
        prompts = self.load_prompts()
        
        print(f"\n🚀 Starting batch generation of {len(prompts)} images")
        print(f"📁 Images will be saved to: {self.assets_path}")
        
        # Convert to list and optionally start from a specific prompt
        prompt_items = list(prompts.items())
        start_index = 0
        
        if start_from:
            try:
                start_index = next(i for i, (key, _) in enumerate(prompt_items) if key == start_from)
                print(f"⏩ Starting from {start_from} (index {start_index})")
            except StopIteration:
                print(f"⚠️ Start prompt '{start_from}' not found, starting from beginning")
        
        successful = 0
        failed = 0
        
        # Process in batches to avoid overwhelming ComfyUI
        for i in range(start_index, len(prompt_items), batch_size):
            batch = prompt_items[i:i + batch_size]
            
            print(f"\n📦 Processing batch {(i // batch_size) + 1} ({len(batch)} items)")
            
            for prompt_key, prompt_content in batch:
                success = self.generate_single_image(prompt_key, prompt_content, workflow)
                
                if success:
                    successful += 1
                else:
                    failed += 1
                
                # Brief pause between items
                time.sleep(1)
            
            # Longer pause between batches
            if i + batch_size < len(prompt_items):
                print(f"⏸️ Pausing 10 seconds before next batch...")
                time.sleep(10)
        
        print(f"\n🎯 Generation complete!")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📁 Check images in: {self.assets_path}")
    
    def generate_specific_prompts(self, prompt_keys):
        """Generate images for specific prompt keys"""
        if not self.check_comfyui_connection():
            print("❌ Cannot connect to ComfyUI. Make sure it's running on http://127.0.0.1:8188")
            return
        
        workflow = self.load_workflow()
        prompts = self.load_prompts()
        
        successful = 0
        failed = 0
        
        for prompt_key in prompt_keys:
            if prompt_key in prompts:
                success = self.generate_single_image(prompt_key, prompts[prompt_key], workflow)
                if success:
                    successful += 1
                else:
                    failed += 1
                time.sleep(1)
            else:
                print(f"⚠️ Prompt key '{prompt_key}' not found")
                failed += 1
        
        print(f"\n🎯 Generation complete!")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
    
    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"🧹 Cleaned up temp directory: {self.temp_dir}")

def main():
    """Main execution function"""
    generator = LafufuGenerator()
    
    try:
        print("🎭 Lafufu ComfyUI Generator")
        print("=" * 50)
        
        # Choose what to generate
        print("\nChoose generation mode:")
        print("1. Generate ALL images (216 total)")
        print("2. Generate specific prompts")
        print("3. Test with first 3 prompts")
        print("4. Resume from specific prompt")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            generator.generate_all_images()
            
        elif choice == "2":
            prompt_keys = input("Enter prompt keys separated by commas (e.g., A0.0V0.6D0.6,A0.2V0.2D0.4): ").strip()
            keys = [k.strip() for k in prompt_keys.split(",") if k.strip()]
            if keys:
                generator.generate_specific_prompts(keys)
            else:
                print("❌ No valid prompt keys provided")
                
        elif choice == "3":
            prompts = generator.load_prompts()
            first_three = list(prompts.keys())[:3]
            print(f"🧪 Testing with: {first_three}")
            generator.generate_specific_prompts(first_three)
            
        elif choice == "4":
            start_prompt = input("Enter prompt key to start from (e.g., A0.4V0.6D0.2): ").strip()
            if start_prompt:
                generator.generate_all_images(start_from=start_prompt)
            else:
                print("❌ No start prompt provided")
                
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n⏹️ Generation interrupted by user")
    
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        generator.cleanup()

if __name__ == "__main__":
    main() 