import { useEffect, useState, useRef } from "react"
import ProjectLink from "./ProjectLink";
import { RxCross1 } from 'react-icons/rx'
import './style.css'
import { TECHNOLOGIES } from '../../test-data';

function showTech(input, str) {
    str = str.toLowerCase().trim();
    input = input.toLowerCase().trim();
    const chars = input.split('')
    for (let i = 0; i < chars.length; i++) {
        if (str.includes(chars[i])) {
            return true;
        }
    }
    return false;
}

export default function ShareYourWorkForm() {

    const [projectLinks, setProjectLinks] = useState([{
        id: new Date().getTime(),
        type: 'Source Code',
        link: '',
    }
    ]);
    const [projectTechnologies, setProjectTechnologies] = useState([]);
    const [suggestedTechnologies, setSuggestedTechnologies] = useState([]);
    const [technologiesInput, setTechnologiesInput] = useState('');

    const handleTechnologiesInput = ({ target }) => {
        setTechnologiesInput(target.value);
        setSuggestedTechnologies(TECHNOLOGIES.filter(tech => showTech(target.value, tech.name) && !projectTechnologies.includes(tech)));
    }

    const inputTagsRef = useRef(null);

    const addToTags = (id) => {
        const target = suggestedTechnologies.filter(tech => tech.id === id)[0];
        suggestedTechnologies.length = 0;
        setProjectTechnologies([...projectTechnologies, target]);
        setTechnologiesInput('');
        inputTagsRef.current.focus();
    }

    const addLink = (e) => {
        e.preventDefault();
        const temp = [...projectLinks];
        temp.push({ type: 'New Link', link: '', id: new Date().getTime() })
        setProjectLinks(temp)
    }

    const removeFromTags = (id) => {
        setProjectTechnologies(projectTechnologies.filter(tech => tech.id !== id));
        inputTagsRef.current.focus();
    }

    const submitShareWork = (e) => {
        e.preventDefault();
        console.log({ projectLinks, projectTechnologies });
    }

    return (
        <>
            <form className="share-work-form">
                <label>Title</label>
                <input type="text" className='main-input' />
                <label>Description</label>
                <textarea className='main-textarea' rows={7} ></textarea>
                <div className="project-links">
                    <h3>Project Links</h3>
                    {
                        projectLinks.map(({ type, link, id }) => <ProjectLink key={id} projectLinks={projectLinks} setProjectLinks={setProjectLinks} id={id} type={type} link={link} />)
                    }
                    <button onClick={addLink} className="add-link-button">New Link</button>
                </div >
                <div className="project-technologies">
                    <h3>Project Technologies</h3>
                    <div className="project-technologies-container">
                        <div className="technologies-tags">
                            {
                                projectTechnologies.map(tech =>
                                    <div key={tech.id} className="technology">
                                        <span>{tech.name}</span>
                                        <button onClick={() => removeFromTags(tech.id)} className='times-button'><span><RxCross1 /></span></button>
                                    </div>
                                )
                            }
                            <input ref={inputTagsRef} onChange={handleTechnologiesInput} value={technologiesInput} type="text" className="main-input" placeholder="e.g. C++, Go..." />
                        </div>
                        {
                            suggestedTechnologies.length !== 0 &&
                            <div className="suggested-techs">
                                <ul>
                                    { suggestedTechnologies.map(tech => <li onClick={() => addToTags(tech.id)} key={tech.id}>{tech.name}</li>) }
                                </ul>
                            </div>
                        }
                    </div>
                </div>
                <button onClick={submitShareWork} className="main-button">Submit</button>
            </form>
        </>
    )
}