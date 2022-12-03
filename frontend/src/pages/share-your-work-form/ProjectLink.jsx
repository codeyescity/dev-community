import { useState } from 'react'
import { RxCross1 } from 'react-icons/rx'

export default function ProjectLink({ projectLinks, setProjectLinks, type, link, id }) {

    // const [inputLink, setInputLink] = useState(link)
    // const [inputType, setInputType] = useState(type)

    function updateLink(attribute, target) {
        setProjectLinks(projectLinks.map(link => {
            if (link.id === id) return ({ ...link, [attribute]: target.value })
            return link;
        }))
    }

    const handleInputType = ({ target }) => {
        // setInputType(target.value);
        updateLink('type', target)
    }

    const handleInputLink = ({ target }) => {
        // setInputLink(target.value);
        updateLink('link', target)
    }

    const removeLink = (e) => {
        e.preventDefault();
        const temp = projectLinks.filter((link) => link.id !== id);
        setProjectLinks(temp)
    }

    return (
        <div className='link'>
            <input type="text" onChange={handleInputType} className='main-input link-type' value={type} />
            <input type="text" onChange={handleInputLink} className='main-input the-link' placeholder="Link Here" value={link} />
            <button className="times-button" onClick={removeLink}><RxCross1 /></button>
        </div>
    )
}