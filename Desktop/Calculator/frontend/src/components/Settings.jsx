import React from 'react'
import './Settings.css'

export default function Settings({ angleMode, setAngleMode, decimalPlaces, setDecimalPlaces, notation, setNotation }) {
  const handleAngleModeChange = async (mode) => {
    setAngleMode(mode)
    try {
      await fetch('/api/config/angle-mode', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ angle_mode: mode })
      })
    } catch (err) {
      console.error('Error updating angle mode:', err)
    }
  }

  const handleDecimalPlacesChange = async (e) => {
    const value = parseInt(e.target.value)
    setDecimalPlaces(value)
    try {
      await fetch('/api/config/decimal-places', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ decimal_places: value })
      })
    } catch (err) {
      console.error('Error updating decimal places:', err)
    }
  }

  const handleNotationChange = async (mode) => {
    setNotation(mode)
    try {
      await fetch('/api/config/notation', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notation: mode })
      })
    } catch (err) {
      console.error('Error updating notation:', err)
    }
  }

  return (
    <div className="settings">
      <div className="setting-group">
        <label>Angle Mode</label>
        <div className="radio-group">
          <label>
            <input
              type="radio"
              value="deg"
              checked={angleMode === 'deg'}
              onChange={(e) => handleAngleModeChange(e.target.value)}
            />
            Degrees
          </label>
          <label>
            <input
              type="radio"
              value="rad"
              checked={angleMode === 'rad'}
              onChange={(e) => handleAngleModeChange(e.target.value)}
            />
            Radians
          </label>
        </div>
      </div>

      <div className="setting-group">
        <label>Decimal Places: {decimalPlaces}</label>
        <input
          type="range"
          min="1"
          max="15"
          value={decimalPlaces}
          onChange={handleDecimalPlacesChange}
          className="slider"
        />
      </div>

      <div className="setting-group">
        <label>Number Notation</label>
        <div className="radio-group">
          <label>
            <input
              type="radio"
              value="standard"
              checked={notation === 'standard'}
              onChange={(e) => handleNotationChange(e.target.value)}
            />
            Standard
          </label>
          <label>
            <input
              type="radio"
              value="scientific"
              checked={notation === 'scientific'}
              onChange={(e) => handleNotationChange(e.target.value)}
            />
            Scientific
          </label>
        </div>
      </div>
    </div>
  )
}
