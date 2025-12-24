import React, { useState } from 'react'
import './Keypad.css'

export default function Keypad({ onNumber, onOperator, onFunction, onDecimal, onParenthesis, onBackspace, onEquals, onClear }) {
  const [advanced, setAdvanced] = useState(false)

  const basicFunctions = ['sin', 'cos', 'tan', 'sqrt', 'log']
  const advancedFunctions = ['asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'log10', 'ln', 'factorial', '!']

  return (
    <div className="keypad">
      {/* Function buttons */}
      <div className="function-row">
        {(advanced ? advancedFunctions : basicFunctions).map(func => (
          <button
            key={func}
            className="btn btn-function"
            onClick={() => onFunction(func)}
          >
            {func}
          </button>
        ))}
      </div>

      {/* Toggle and Special buttons */}
      <div className="control-row">
        <button className="btn btn-toggle" onClick={() => setAdvanced(!advanced)}>
          {advanced ? 'Basic' : '2nd'}
        </button>
        <button className="btn btn-special" onClick={() => onParenthesis('(')}>( </button>
        <button className="btn btn-special" onClick={() => onParenthesis(')')}>)</button>
        <button className="btn btn-clear" onClick={onClear}>AC</button>
        <button className="btn btn-delete" onClick={onBackspace}>⌫</button>
      </div>

      {/* Number pad */}
      <div className="number-grid">
        {[7, 8, 9].map(num => (
          <button key={num} className="btn btn-number" onClick={() => onNumber(num)}>
            {num}
          </button>
        ))}
        <button className="btn btn-operator" onClick={() => onOperator('/')}>÷</button>
        <button className="btn btn-operator" onClick={() => onOperator('%')}>%</button>

        {[4, 5, 6].map(num => (
          <button key={num} className="btn btn-number" onClick={() => onNumber(num)}>
            {num}
          </button>
        ))}
        <button className="btn btn-operator" onClick={() => onOperator('*')}>×</button>
        <button className="btn btn-operator" onClick={() => onOperator('^')}>^</button>

        {[1, 2, 3].map(num => (
          <button key={num} className="btn btn-number" onClick={() => onNumber(num)}>
            {num}
          </button>
        ))}
        <button className="btn btn-operator" onClick={() => onOperator('-')}>−</button>
        <button className="btn btn-equals" onClick={onEquals}>=</button>

        <button className="btn btn-number zero" onClick={() => onNumber(0)}>0</button>
        <button className="btn btn-number" onClick={onDecimal}>.</button>
        <button className="btn btn-operator" onClick={() => onOperator('+')}>+</button>
      </div>
    </div>
  )
}
