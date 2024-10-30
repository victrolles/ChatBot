import React from 'react'

import chatbot_logo from '../assets/logo.png'

const Message = () => {
  return (
    <div className='message owner'>
        <div className="messageInfo">
            <img src={chatbot_logo} alt="chatbot logo" />
        </div>
        <div className="messageContent">
            <p> I love computer science</p>
        </div>
    </div>
  )
}

export default Message