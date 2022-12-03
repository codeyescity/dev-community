import { useEffect, useRef } from 'react'
import './style.css'

export default function Model({ model, closeModel, modelHeading, children }) {

    const overlayRef = useRef(null);

    useEffect(() => {

        const listener = () => closeModel(false);

        overlayRef.current.addEventListener('click', listener);

        return () => overlayRef.current?.removeEventListener('click', listener);
    }, []);

    return (
        <>
            <div ref={overlayRef} className="overlay"></div>
            <div className="model">
                <h3>{ modelHeading }</h3>
                {children}
            </div>
        </>
    )
}