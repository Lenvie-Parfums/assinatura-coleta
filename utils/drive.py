import datetime
import json
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import streamlit as st


# Carregar credenciais da conta de serviço
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_pdf_google_drive(pdf_bytes, nome_arquivo):

    info = json.loads(st.secrets["gcp"]["service_account"])
    # Autentica
    credentials = service_account.Credentials.from_service_account_info(
        info, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    # ID do drive compartilhado
    shared_drive_id = st.secrets["gcp"]["shared_drive_id"]  # Adiciona isso no secrets.toml

    # ID da pasta raiz dentro do Shared Drive
    pasta_raiz_id = st.secrets["gcp"]["pasta_id"]

    data_str = datetime.datetime.now().strftime('%d/%m/%Y')

    results = service.files().list(
        q=f"'{pasta_raiz_id}' in parents and name='{data_str}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        driveId=pasta_raiz_id,
        corpora='drive',
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        fields='files(id, name)'
    ).execute()

    files = results.get('files', [])

    if files:
        pasta_data_id = files[0]['id']
    else:
        # Cria nova pasta dentro do Shared Drive
        folder_metadata = {
            'name': data_str,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [pasta_raiz_id],
            'driveId': shared_drive_id
        }
        folder = service.files().create(
            body=folder_metadata,
            fields='id',
            supportsAllDrives=True
        ).execute()
        pasta_data_id = folder.get('id')

    # Upload do PDF para a pasta correta
    media = MediaIoBaseUpload(pdf_bytes, mimetype='application/pdf')
    file_metadata = {
        'name': nome_arquivo,
        'parents': [pasta_data_id],
        'driveId': shared_drive_id,
        'mimeType': 'application/pdf'
    }

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink',
        supportsAllDrives=True
    ).execute()

    return file.get('webViewLink')

