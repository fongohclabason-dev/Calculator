import React from 'react'
import './History.css'

export default function History({ items, onSelect }) {
  if (!items || items.length === 0) {
    return <div className="history-empty">No history yet</div>
  }

  return (
    <div className="history">
      <h3>History</h3>
      <div className="history-list">
        {items.slice(0, 5).map((item, index) => (
          <div
            key={index}
            className="history-item"
            onClick={() => onSelect(item)}
          >
            <span className="history-expr">{item.expression}</span>
            <span className="history-result">{item.result}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
