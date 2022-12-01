import { createContext, useContext, useReducer, useState } from 'react'
import { initialState } from './initialState'
import { reducer } from './reducer';

const globalStateContext = createContext();
export const useGlobalState = () => useContext(globalStateContext);


export default function GlobalStateProvider({ children }) {

    const[state, dispatch] = useReducer(reducer, initialState);

    return (
        <globalStateContext.Provider value={{ state, dispatch }}>
            { children }
        </globalStateContext.Provider>
    )
}