import React from 'react'

const Input = () => {
  return (
    <div className='chat-input'>
        <input type="text" placeholder="Type a message..." />
        <button>Send</button>
    </div>
  )
}

export default Input