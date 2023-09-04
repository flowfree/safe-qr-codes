export interface QRCode {
  image: string
  data: string
}

interface Props {
  QRCodes: QRCode[]
}

export default function DisplayResult({ QRCodes }: Props) {
  return (
    <>
      {QRCodes.length > 0 && (
        <ul>
          {QRCodes.map((item, index) => (
            <li key={index}>
              <div>
                <img src={`data:image/png;base64,${item.image}`} className="w-[100px]" alt="" />
                <p>{item.data}</p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </>
  )
}
