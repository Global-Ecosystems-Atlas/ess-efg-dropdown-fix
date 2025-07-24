import os
import requests
import sys
from pprint import pprint

def main():

    # Define parameters
    new_efgs = ['EFG_CODE']  # e.g: ['F_1_3_FREEZE-THAW_RIVERS_AND_STREAMS'] or ['FM_1_3_INTERMITTENTLY_CLOSED_AND_OPEN_LAKES_AND_LAGOONS, MT_1_1_ROCKY_SHORELINES']
    project_id = 'project-id'
    metadata_names = ['iucn_efg_code_dominant_100m', 'iucn_efg_code_secondary_10m', 'iucn_efg_code_secondary_100m']  # e.g: 'efg_100m' or 'efg2_10m'


    # Set up the API key and request headers
    if not os.path.exists('api_key.txt'):
        print("API key not found. Please create an 'api_key.txt' file and paste your API key inside.")
        sys.exit(1)

    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}


    # Retrieve the metadata IDs
    # /!\ At least one annotation must have been defined with these metadata beforehand /!\
    r = requests.get(f'https://earth-system-studio.allen.ai/api/v1/projects/{project_id}/metadata-report', headers=headers)
    r.raise_for_status()

    metadata_list = r.json()

    metadata_ids = []

    for name in metadata_names:
        found = False
        for item in metadata_list:
            if item.get('metadata_name') == name:
                metadata_ids.append(item.get("metadata_id"))
                found = True
                break

        if not found:
            print(f"Metadata '{name}' not found.")
            sys.exit(1)


    # Retrieve the metadata and update their allowed values
    for i, (metadata_id, metadata_name) in enumerate(zip(metadata_ids, metadata_names), start=1):

        msg_start = f"[{i}/{len(metadata_ids)}]"


        # Retrieve the metadata
        r = requests.get(f'https://earth-system-studio.allen.ai/api/v1/annotation_metadata_fields/{metadata_id}', headers=headers)
        r.raise_for_status()
        metadata = r.json()
        
        if metadata.get('data_type') != 'enum':
            print(f"{msg_start} Skipping metadata '{metadata_name}' because it is not a dropdown list (enum).")
            continue


        # Add new EFG codes to the metadata field
        added_efgs = []
        already_present_efgs = []

        for new_efg in new_efgs:
            if new_efg not in metadata['allowed_values']:
                metadata['allowed_values'].append(new_efg)
                added_efgs.append(new_efg)
            else:
                already_present_efgs.append(new_efg)

        metadata['allowed_values'] = sorted(metadata['allowed_values'])


        # Update the metadata field
        response = requests.put(f'https://earth-system-studio.allen.ai/api/v1/annotation_metadata_fields/{metadata_id}', json=metadata, headers=headers)

        if response.status_code == 200:
            print(f"{msg_start} Metadata '{metadata_name}' updated successfully.")
            spaces = " " * len(msg_start)

            if added_efgs:
                print(f"{spaces} EFGs added: {', '.join(added_efgs)}.")

            if already_present_efgs:
                print(f"{spaces} EFGs already present: {', '.join(already_present_efgs)}.")
        else:
            print(f"{msg_start} Failed to update metadata '{metadata_name}'. Status code {response.status_code}: {response.text}")


if __name__ == "__main__":
    main()


# api/v1/projects/{project_id}/tag-report           
# → only shows tags assigned to annotations, not all tags in a project.

# api/v1/projects/{project_id}/metadata-report      
# → only shows metadata fields if they are assigned to at least one annotation.