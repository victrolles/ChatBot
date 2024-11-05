import React from 'react'

import chatbot_logo from '../assets/logo.png'

const NewChat = () => {
  return (
    <div className='newChat'>
        <img src={chatbot_logo} alt='logo chatbot'></img>
        <p>Start a new chat</p>
    </div>
  )
}

export default NewChat