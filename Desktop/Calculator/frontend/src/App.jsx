import React, { useState, useEffect } from 'react'
import Display from './components/Display'
import Keypad from './components/Keypad'
import History from './components/History'
import Settings from './components/Settings'
import './App.css'

export default function App() {
  const [expression, setExpression] = useState('')
  const [display, setDisplay] = useState('0')
  const [memory, setMemory] = useState(0)
  const [history, setHistory] = useState([])
  const [angleMode, setAngleMode] = useState('deg')
  const [decimalPlaces, setDecimalPlaces] = useState(6)
  const [notation, setNotation] = useState('standard')
  const [justCalculated, setJustCalculated] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  // Fetch initial config from backend
  useEffect(() => {
    fetchConfig()
    fetchHistory()
  }, [])

  const fetchConfig = async () => {
    try {
      const res = await fetch('/api/config')
      const data = await res.json()
      setAngleMode(data.angle_mode || 'deg')
      setDecimalPlaces(data.decimal_places || 6)
      setNotation(data.notation || 'standard')
    } catch (err) {
      console.error('Error fetching config:', err)
    }
  }

  const fetchHistory = async () => {
    try {
      const res = await fetch('/api/history')
      const data = await res.json()
      setHistory(data.history || [])
    } catch (err) {
      console.error('Error fetching history:', err)
    }
  }

  const handleNumber = (num) => {
    if (justCalculated) {
      setExpression(String(num))
      setDisplay(String(num))
      setJustCalculated(false)
    } else {
      const newExpression = expression + String(num)
      setExpression(newExpression)
      setDisplay(newExpression)
    }
  }

  const handleOperator = (op) => {
    if (justCalculated) {
      setExpression(display + op)
      setDisplay(op)
      setJustCalculated(false)
    } else if (expression && !expression.endsWith('+') && !expression.endsWith('-') && !expression.endsWith('*') && !expression.endsWith('/') && !expression.endsWith('^') && !expression.endsWith('%')) {
      setExpression(expression + op)
      setDisplay(op)
    }
  }

  const handleFunction = (func) => {
    const lastOperatorIndex = Math.max(
      expression.lastIndexOf('+'),
      expression.lastIndexOf('-'),
      expression.lastIndexOf('*'),
      expression.lastIndexOf('/'),
      expression.lastIndexOf('^'),
      expression.lastIndexOf('%')
    )
    
    const currentNumber = lastOperatorIndex === -1 ? expression : expression.substring(lastOperatorIndex + 1)
    
    if (!currentNumber || currentNumber.match(/[+\-*/%^]/)) {
      setExpression(expression + func + '(')
      setDisplay(func + '(')
    } else {
      const beforeNumber = expression.substring(0, lastOperatorIndex + 1)
      const newExpression = beforeNumber + func + '(' + currentNumber + ')'
      setExpression(newExpression)
      setDisplay(func + '(' + currentNumber + ')')
    }
  }

  const handleDecimal = () => {
    const lastOperatorIndex = Math.max(
      expression.lastIndexOf('+'),
      expression.lastIndexOf('-'),
      expression.lastIndexOf('*'),
      expression.lastIndexOf('/'),
      expression.lastIndexOf('^'),
      expression.lastIndexOf('%')
    )
    
    const currentNumber = lastOperatorIndex === -1 ? expression : expression.substring(lastOperatorIndex + 1)
    
    if (!currentNumber.includes('.')) {
      const newExpression = expression + '.'
      setExpression(newExpression)
      setDisplay(newExpression)
    }
  }

  const handleParenthesis = (paren) => {
    let newExpression = expression + paren
    
    if (paren === '(') {
      setExpression(newExpression)
      setDisplay(newExpression)
    } else if (paren === ')') {
      const openCount = (newExpression.match(/\(/g) || []).length
      const closeCount = (newExpression.match(/\)/g) || []).length
      
      if (closeCount < openCount) {
        setExpression(newExpression)
        setDisplay(newExpression)
      }
    }
  }

  const handleBackspace = () => {
    if (justCalculated) {
      setExpression('')
      setDisplay('0')
      setJustCalculated(false)
    } else {
      const newExpression = expression.slice(0, -1)
      setExpression(newExpression)
      setDisplay(newExpression || '0')
    }
  }

  const handleEquals = async () => {
    if (!expression) return

    // Validate expression
    const openParens = (expression.match(/\(/g) || []).length
    const closeParens = (expression.match(/\)/g) || []).length
    if (openParens !== closeParens) {
      setDisplay('Error: Unmatched parentheses')
      return
    }

    if (/[+\-*/%^]$/.test(expression)) {
      setDisplay('Error: Incomplete expression')
      return
    }

    try {
      const res = await fetch('/api/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          expression,
          angle_mode: angleMode,
          decimal_places: decimalPlaces,
          notation
        })
      })
      
      const data = await res.json()
      
      if (data.error) {
        setDisplay(`Error: ${data.error}`)
      } else {
        const result = data.result
        setDisplay(String(result))
        setExpression(String(result))
        setJustCalculated(true)
        setHistory([{ expression, result }, ...history])
      }
    } catch (err) {
      setDisplay('Error: Connection failed')
      console.error('Calculate error:', err)
    }
  }

  const handleClear = () => {
    setExpression('')
    setDisplay('0')
    setJustCalculated(false)
  }

  const handleMemoryAdd = async () => {
    try {
      await fetch('/api/memory/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: parseFloat(display) })
      })
      const res = await fetch('/api/memory')
      const data = await res.json()
      setMemory(data.value)
    } catch (err) {
      console.error('Memory error:', err)
    }
  }

  const handleMemoryClear = async () => {
    try {
      await fetch('/api/memory/clear', { method: 'DELETE' })
      setMemory(0)
    } catch (err) {
      console.error('Memory error:', err)
    }
  }

  const handleHistoryClick = (item) => {
    setExpression(item.expression)
    setDisplay(item.expression)
    setJustCalculated(false)
  }

  return (
    <div className="app-container">
      <div className="calculator">
        <div className="header">
          <h1>Scientific Calculator</h1>
          <button className="settings-btn" onClick={() => setShowSettings(!showSettings)}>⚙️</button>
        </div>

        {showSettings && (
          <Settings
            angleMode={angleMode}
            setAngleMode={setAngleMode}
            decimalPlaces={decimalPlaces}
            setDecimalPlaces={setDecimalPlaces}
            notation={notation}
            setNotation={setNotation}
          />
        )}

        <Display 
          display={display} 
          memory={memory}
          onMemoryAdd={handleMemoryAdd}
          onMemoryClear={handleMemoryClear}
        />

        <Keypad
          onNumber={handleNumber}
          onOperator={handleOperator}
          onFunction={handleFunction}
          onDecimal={handleDecimal}
          onParenthesis={handleParenthesis}
          onBackspace={handleBackspace}
          onEquals={handleEquals}
          onClear={handleClear}
        />

        <History items={history} onSelect={handleHistoryClick} />
      </div>
    </div>
  )
}
