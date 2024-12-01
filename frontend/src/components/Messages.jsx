import { React, useEffect, useState } from 'react'
import Message from './Message'
import { useChat } from '../context/ChatContext'
import axios from 'axios'

const Messages = () => {

  const [messages, setMessages] = useState([])

  const { chatId, trigger } = useChat()

  useEffect(() => {
    if (chatId) {
        axios.post('http://localhost:5000/getMessagesFromChat', { chatId: chatId })
            .then(res => {
                if (res.status === 200) {
                  setMessages(res.data);  // Store the chats in the state
                    console.log('Messages retrieved:', res.data);
                } else {
                    console.log('No messages found');
                }
            })
            .catch(err => console.error('Error fetching messages:', err));
    }
  }, [chatId, trigger]);

  return (
    <div className='messages'>
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
    </div>
  )
}

export default Messages