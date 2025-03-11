# main.py
import sys
import json
from video_processor import extract_frames
from openai_vision_integration import get_image_files, encode_image, analyze_room_images
from price_estimator import estimate_prices

# Hardcoded video file
VIDEO_PATH = "my-video.MOV"
FRAME_OUTPUT_FOLDER = "./videoFrames"

def main():
    print("Starting video processing...")
    extract_frames(VIDEO_PATH, FRAME_OUTPUT_FOLDER, interval_seconds=2)  # Extracts frames every 10 frames
    print(f"Frames saved in {FRAME_OUTPUT_FOLDER}")

    # Retrieve extracted frames
    image_files = get_image_files(FRAME_OUTPUT_FOLDER)
    if not image_files:
        print("No images found in extracted frames!")
        return

    print(f"Found {len(image_files)} frame(s): {image_files}")

    # Encode images to Base64
    encoded_images = [encode_image(img) for img in image_files if encode_image(img)]
    print(f"Encoded {len(encoded_images)} images for OpenAI processing.")

    # Define prompt for asset detection
    room_analysis_prompt = (
        "You are analyzing images of a room for home asset management purposes. Your task is to:\n"
        "1. Identify all unique assets visible in the room that people might want to log in a home inventory system.\n"
        "2. Include items such as furniture, electronics, appliances, decor, and other valuable assets.\n"
        "3. For each asset, provide the following details in JSON format:\n"
        "   - Asset Type (e.g., Sofa, TV, Lamp, Stovetop, Washing Machine, Painting)\n"
        "   - Category (choose one of the following): Furniture, Vehicles, Tools, Structure, Electronics, Safety, Equipment, Appliances, Valuables, Other.\n"
        "   - Sub-Category (choose one from the specific sub-categories listed under each category below, or default to 'Other' if no match is found):\n"
        "   - Color:\n"
        "4. If an asset does not align with any of the specific sub-categories listed, assign the sub-category 'Other'.\n"
        "5. Ensure no duplicate items. If the same asset is visible in multiple images, consolidate the information into one entry, enriching it with details from each image.\n\n"
        "Respond only with a JSON array containing the consolidated list of unique assets."
    )

    # Send images to OpenAI API for asset detection
    print("Sending images to OpenAI API for asset detection...")
    openai_response = analyze_room_images(encoded_images, room_analysis_prompt)
    if not openai_response:
        print("ERROR: OpenAI API response is empty!")
        return

    try:
        # Parse JSON response from OpenAI
        asset_list = json.loads(openai_response.choices[0].message.content)
        print(f"Successfully parsed OpenAI response: {len(asset_list)} assets found.")
    except Exception as e:
        print(f"ERROR: Failed to parse OpenAI response! {e}")
        return

    print("Assets detected:", json.dumps(asset_list, indent=2))

    # Step 3: Get price estimates from SerpAPI
    print("Querying SerpAPI for asset pricing...")
    priced_assets = estimate_prices(asset_list)

    # Final Output
    print("Final asset list with price estimates:")
    print(json.dumps(priced_assets, indent=2))

if __name__ == "__main__":
    main()
