import React from 'react'
import Messages from './Messages'
import Input from './Input'

const Chat = () => {
  return (
    <div className='chat'>
        <div className="chat-header">
            <span className="title">Computer science</span>
        </div>
        <Messages />
        <Input />
    </div>
  )
}

export default Chat