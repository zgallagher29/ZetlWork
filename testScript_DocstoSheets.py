## source link: https://developers.google.com/drive/api/v3/integrate-open#open_and_convert_google_docs_in_your_app

file_id = '1ZdR3L3qP4Bkq8noWLJHSr_iBau0DNT4Kli4SxNc2YEo'
request = drive_service.files().export_media(fileId=file_id,
                                             mimeType='application/pdf')
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print "Download %d%%." % int(status.progress() * 100)