import React from 'react'
import Navbar from './Navbar'
import Chats from './Chats'
import NewChats from './NewChats'

const Sidebar = () => {
  return (
    <div className='sidebar'>
        <Navbar />
        <Chats />
        <NewChats />
    </div>
  )
}

export default Sidebar