# IPTV Playlist Generator

This tool fetches a remote M3U playlist, filters it, and reorganizes the channels according to specific preferences.

## Features

- **Fetch & Retry**: Downloads the playlist from a configured source with automatic retry logic (up to 2 retries).
- **Validation**: Ensures the fetched playlist is valid and contains sufficient data (minimum 100 lines).
- **Group Filtering**: Selects and organizes channels based on a predefined list of groups (e.g., Overseas, Taiwan, Hong Kong/Macau).
- **Reordering**: Sorts channels based on the `GROUP_ORDER` priority.
- **Clean Output**: Generates a finalized `tv.m3u` file ready for use.

## Configuration

- **Source URL**: `https://tv.iill.top/m3u/Gather`
- **Output File**: `tv.m3u`

## Usage

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Script**:
   ```bash
   python gen_m3u.py
   ```

## Processing Logic

1. **Fetch**: Downloads the M3U content from the source URL.
2. **Match**: Iterates through the playlist and matches channels to the defined `GROUP_ORDER`.
3. **Save**: Writes the matched channels to the output file in the specified order.
# IPTV2
