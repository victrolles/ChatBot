import React from 'react'
import Messages from './Messages'
import NewChat from './NewChat'
import Input from './Input'

import { useChat } from '../context/ChatContext'

const Chat = () => {

  const { chatId, chatName } = useChat()
  console.log('Chat ID:', chatId);

  return (
    <div className='chat'>
        <div className="chat-header">
            <span className="title">{chatName}</span>
        </div>
        {chatId ? <Messages /> : <NewChat />}
        <Input />
    </div>
  )
}

export default Chat