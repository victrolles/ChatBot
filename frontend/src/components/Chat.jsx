import React from 'react'
import Messages from './Messages'
import Input from './Input'

import { useChat } from '../context/ChatContext'

const Chat = () => {

  const { chatName } = useChat()

  return (
    <div className='chat'>
        <div className="chat-header">
            <span className="title">{chatName}</span>
        </div>
        <Messages />
        <Input />
    </div>
  )
}

export default Chat