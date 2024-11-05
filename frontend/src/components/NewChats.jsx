import React from 'react'
import { useChat } from '../context/ChatContext'


const NewChats = () => {

    const { unsub } = useChat()

    return (
        <div className='newChats'>
            <button onClick={() => unsub()}>Start a new chat</button>
        </div>
    )
}

export default NewChats