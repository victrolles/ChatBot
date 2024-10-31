import { createContext, useContext, useState } from 'react';

export const ChatContext = createContext();

export const ChatContextProvider = ({ children }) => {
    const [chatId, setChatId] = useState(null);
    const [chatName, setChatName] = useState(null);  // New state for chatName

    const sub = ({ id, name }) => {  // Destructure id and name from the chat object
        setChatId(id);
        setChatName(name);
    };

    const unsub = () => {
        setChatId(null);
        setChatName(null);  // Clear chatName as well on unsubscribe
    };

    return (
        <ChatContext.Provider value={{ chatId, chatName, sub, unsub }}>
            {children}
        </ChatContext.Provider>
    );
};

export const useChat = () => useContext(ChatContext);
