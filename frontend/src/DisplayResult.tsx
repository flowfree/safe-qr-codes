export interface QRCode {
  image: string
  data: string
  isSafe: boolean
  threatDetails: string[]
}

interface Props {
  QRCodes: QRCode[]
}

export default function DisplayResult({ QRCodes }: Props) {
  return (
    <div>
      <ul>
        {QRCodes.map((item, index) => (
          <li key={index} className="flex gap-4 my-4 first:mt-0 last:mb-0">
            <img src={`data:image/png;base64,${item.image}`} className="w-[100px]" alt="" />
            <div>
              <p className="mb-2">
                <a href={item.data} className={'hover:underline ' + (item.isSafe ? 'text-green-700' : 'text-red-700')} target="_blank">
                  {item.data}
                </a>
              </p>
              {item.isSafe && (
                <span className="py-1 px-2 rounded-md bg-green-100 text-green-700 font-bold">
                  SAFE
                </span>
              )}
              {item.threatDetails && (
                item.threatDetails.map((item, index) => (
                  <span key={index} className="py-1 px-2 rounded-md bg-red-100 text-red-700 font-bold">
                    {item}
                  </span>
                ))
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
