import React from "react"
import './index.css';

function Seasons(props) {
    let string = "Temporada "
    let string2 = "Episodio "
    let aux = []
    Object.keys(props.episodes).forEach(key => {
        let value = props.episodes[key];
        if (props.season === value.season) {
            aux.push(
                <button className="small-buttons" onClick={event => props.episodeClick(event, value.episode_id)}> 
                {value.episode ? string2 + value.episode + ": " + value.title : null} 
                </button>
            )
            aux.push(<br/>)
        }
    })
      
    return (
        <div>
            <button className="collapsible"> {props.season ? string + props.season : null} </button>
            <div>{aux}</div>
        </div>
    )

}

export default Seasons