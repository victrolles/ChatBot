import React, { useEffect, useRef } from 'react'

import chatbot_logo from '../assets/logo.png'
import user_logo from '../assets/user-icon.png'

const Message = (message) => {

  const ref = useRef()

  useEffect(() => {
    ref.current.scrollIntoView({ behavior: 'smooth' })
  }, [message])

  return (
    <div ref={ref} className={`message ${message.message.bot === 0 ? "owner" : ""}`}>
        <div className="messageInfo">
            <img src={
                message.message.bot === 0 ? user_logo : chatbot_logo
            } alt="chatbot logo" />
        </div>
        <div className="messageContent">
            <p>{message.message.content}</p>
        </div>
    </div>
  )
}

export default Message