import { React, useState } from 'react'
import { useChat } from '../context/ChatContext'
import axios from 'axios'

const Input = () => {

  const { chatId } = useChat()
  const [text, setText] = useState('')

  const handleSend = () => {

    if (text) {
      axios.post('http://localhost:8081/sendMessage', { chatId: chatId, content: text })
        .then(res => {
          if (res.status === 200) {
            console.log('Message sent:', res.data);
          } else {
            console.log('Message not sent');
          }
        })
        .catch(err => console.error('Error sending message:', err));
    }
  }

  return (
    <div className='chat-input'>
        <input type="text" placeholder="Type a message..." onChange={e=>setText(e.target.value)} />
        <button onClick={handleSend}>Send</button>
    </div>
  )
}

export default Input