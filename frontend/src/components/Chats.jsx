import React, { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { useChat } from '../context/ChatContext'
import axios from 'axios'

const Chats = () => {

    const [chats, setChats] = useState([])

    const { user } = useAuth()
    const { sub, trigger } = useChat()

    useEffect(() => {
        if (user) {
            axios.post('http://localhost:8081/getChatsFromUser', { name: user.name })
                .then(res => {
                    if (res.status === 200) {
                        setChats(res.data);  // Store the chats in the state
                        console.log('Chats retrieved:', res.data);
                    } else {
                        console.log('No chats found');
                    }
                })
                .catch(err => console.error('Error fetching chats:', err));
        }
    }, [user, trigger]);

    const handleSelect = (chatId, chatName) => {
        sub({ id: chatId, name: chatName });
    }

    return (
        <div className='chats'>
            {chats.map((chat) => (
                <div className="userChat" key={chat.chatId} onClick={() => handleSelect(chat.chatId, chat.chatName)}>
                    <span className="title">{chat.chatName}</span>
                    <span className="lastMessage">{chat.lastMessage}</span>
                </div>
            ))}
        </div>
    )
}

export default Chats