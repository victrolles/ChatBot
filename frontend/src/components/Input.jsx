import { React, useEffect, useState } from 'react'
import { useChat } from '../context/ChatContext'
import { useAuth } from '../context/AuthContext'
import axios from 'axios'

const Input = () => {

  const { chatId, refresh, sub } = useChat()
  const { user } = useAuth()
  const [text, setText] = useState('')

  const handleSend = () => {

    if (text) {

      if (!chatId) {

        axios.post('http://localhost:5000/createChat', { email: user.name, content: text })
        .then(res => {
          if (res.status === 200) {

            console.log('Chat created:', res.data);

            axios.post('http://localhost:5000/sendMessage', { chatId: res.data.id, content: text })
            .then(res => {
              if (res.status === 200) {
                console.log('Message sent:', res.data);
                refresh();
              } else {
                console.log('Message not sent');
              }
            })
            .catch(err => console.error('Error sending message:', err));

            sub({ id: res.data.id, name: res.data.name });

          } else {
            console.log('Chat not created');
          }
        })

      } else {

        axios.post('http://localhost:5000/sendMessage', { chatId: chatId, content: text })
        .then(res => {
          if (res.status === 200) {
            console.log('Message sent:', res.data);
            refresh();
          } else {
            console.log('Message not sent');
          }
        })
        .catch(err => console.error('Error sending message:', err));
        
      }

      setText(''); // Clear input after sending

    }
  }

  return (
    <div className='chat-input'>
        <input type="text" value={text} placeholder="Type a message..." onChange={e=>setText(e.target.value)} />
        <button onClick={handleSend}>Send</button>
    </div>
  )
}

export default Input