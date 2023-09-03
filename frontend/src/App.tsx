import FileUpload from './FileUpload'

function App() {

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold tracking-tight">
        Safe QR Codes
      </h1>
      <p>
        This application will scan the QR codes in your documents and check if they
        contain safe or unsafe URLs. 
      </p>
      <FileUpload />
    </div>
  )
}

export default App
