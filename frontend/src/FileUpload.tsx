import React, { useState } from 'react'
import axios from 'axios'
import DisplayResult, { QRCode } from './DisplayResult'

const baseURL = import.meta.env.VITE_API_BASE_URL

export default function FileUpload() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [progress, setProgress] = useState<number>(0)
  const [data, setData] = useState<QRCode[]>([])

  function triggerFileInput() {
    const fileInput = document.getElementById('fileInput')
    if (fileInput) {
      fileInput.click()
    }
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      uploadFile(file)
    }
  }

  async function uploadFile(file: File) {
    const formData = new FormData()
    formData.append('file', file)

    setData([])

    try {
      const { data } = await axios.post(`${baseURL}/upload_file`, formData, {
        onUploadProgress: (progressEvent) => {
          let percentage = 0
          if (progressEvent.total) {
            percentage = (progressEvent.loaded / progressEvent.total) * 100
          }
          setProgress(percentage)
        },
      })

      setData(data)
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div>
      <input
        id="fileInput"
        type="file"
        accept=".pdf,.docx,.jpg,.jpeg,.png" 
        className="hidden"
        onChange={handleFileChange}
      />
      <button 
        className="py-1 px-4 shadow-md rounded-md bg-indigo-600 text-white hover:bg-indigo-500"
        onClick={triggerFileInput}
      >
        Select File
      </button>
      {selectedFile && (
        <p>Uploading {selectedFile.name} ({progress.toFixed(0)}%)</p>
      )}
      <DisplayResult QRCodes={data} />
    </div>
  )
}
