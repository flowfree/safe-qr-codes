import Counter from './Counter'
import './App.css'

function App() {

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold">
        Hello, World!
      </h1>
      <p className="py-4">
        Vite (French word for "quick", pronounced /vit/, like "veet") is a build tool that aims to provide a faster and leaner development experience for modern web projects.
      </p>
      <Counter />
    </div>
  )
}

export default App
