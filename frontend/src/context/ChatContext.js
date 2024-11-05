import { createContext, useContext, useState } from 'react';

export const ChatContext = createContext();

export const ChatContextProvider = ({ children }) => {
    const [chatId, setChatId] = useState(null);
    const [chatName, setChatName] = useState(null);
    const [trigger, setTrigger] = useState(false);

    const sub = ({ id, name }) => {  // Destructure id and name from the chat object
        setChatId(id);
        setChatName(name);
    };

    const unsub = () => {
        setChatId(null);
        setChatName(null);  // Clear chatName as well on unsubscribe
    };

    const refresh = () => {
        setTrigger(!trigger);
    };

    return (
        <ChatContext.Provider value={{ chatId, chatName, trigger, sub, unsub, refresh }}>
            {children}
        </ChatContext.Provider>
    );
};

export const useChat = () => useContext(ChatContext);
