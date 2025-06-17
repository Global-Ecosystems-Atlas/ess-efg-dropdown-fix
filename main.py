import os
import requests
import sys
from pprint import pprint

def main():

    # Define parameters
    new_efgs = ['F_1_3_FREEZE-THAW_RIVERS_AND_STREAMS']  # e.g: ['F_1_3_FREEZE-THAW_RIVERS_AND_STREAMS'] or ['FM_1_3_INTERMITTENTLY_CLOSED_AND_OPEN_LAKES_AND_LAGOONS, MT_1_1_ROCKY_SHORELINES']
    project_id = 'baa637ae-4ed6-4989-9e31-6829379238ff'
    metadata_name = 'iucn_efg_code_100m'  # e.g: 'efg_100m' or 'efg2_10m'


    # Set up the API key and request headers
    if not os.path.exists('api_key.txt'):
        print("API key not found. Please create an 'api_key.txt' file and paste your API key inside.")
        sys.exit(1)

    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}


    # Retrieve the ID of the metadata field
    # /!\ At least one annotation must have been defined beforehand /!\
    r = requests.get(f'https://earth-system-studio.allen.ai/api/v1/projects/{project_id}/metadata-report', headers=headers)
    r.raise_for_status()

    metadata_list = r.json()

    metadata_id = None

    for item in metadata_list:
        if item.get('metadata_name') == metadata_name:
            metadata_id = item.get('metadata_id')
            break

    if metadata_id is None:
        print(f"Identifier for the metadata '{metadata_name}' not found.")
        sys.exit(1)

    
    # Retrieve the metadata field 
    r = requests.get(f'https://earth-system-studio.allen.ai/api/v1/annotation_metadata_fields/{metadata_id}', headers=headers)
    r.raise_for_status()

    metadata = r.json()
    
    if metadata.get('data_type') != 'enum':
        print("The metadata you are trying to modify is not a dropdown list.")
        sys.exit(1)

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
        print(f"Metadata updated successfully.")

        if added_efgs:
            print(f"EFGs added: {', '.join(added_efgs)}.")

        if already_present_efgs:
            print(f"EFGs already present: {', '.join(already_present_efgs)}.")
    else:
        print(f"Failed to update metadata. Status code {response.status_code}: {response.text}")


if __name__ == "__main__":
    main()


# api/v1/projects/{project_id}/tag-report           
# → only shows tags assigned to annotations, not all tags in a project.

# api/v1/projects/{project_id}/metadata-report      
# → only shows metadata fields if they are assigned to at least one annotation.