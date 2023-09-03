import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)

  return (
    <>
      <button
        className="py-2 px-4 shadow-md rounded-md bg-indigo-600 text-white disabled:bg-gray-400 disabled:text-gray-100"
        disabled={count === 0}
        onClick={e => setCount(count-1)}
      >
        Decrement
      </button>
      <span className="mx-4">
        { count }
      </span>
      <button
        className="py-2 px-4 shadow-md rounded-md bg-indigo-600 text-white"
        onClick={e => setCount(count+1)}
      >
        Increment
      </button>
    </>
  )
}
