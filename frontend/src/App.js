import { useEffect, useState } from 'react';
import script from './python/script.py';
import logo from './logo.svg';
import './App.css';

function App() {
  const [output, setOutput] = useState("(loading...)");

  const runScript = code => {
    window.pyodide.globals.set("data", '1234');

    window.pyodide.loadPackage([]).then(() => {
      const output = window.pyodide.runPython(code);
      setOutput(output);
    })
  }


  const calculate = () => {
    console.log("calculate ");

    window.languagePluginLoader.then(() => {
      fetch(script)
        .then(src => src.text())
        .then(runScript)
    })

  }

  return (
    <div className="App">
      <div>
        test
      </div>
      <p>
        output: {output}
      </p>
      <button onClick={() => calculate()}>
        run Python
      </button>
    </div>
  );
}

export default App;
