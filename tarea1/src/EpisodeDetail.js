import React from "react"
import CharacterDetails from "./CharacterDetails"

class EpisodeDetail extends React.Component {

    constructor(props) {
        super(props)
        this.state = {}
    }

    async componentDidMount() {
        let all_characters = []
        for (let character of this.props.value.characters) {
            let string = "https://tarea-1-breaking-bad.herokuapp.com/api/characters?name="
            let name = character.replace(/ /g, "+")
            string += name
            await fetch(string)
                .then(response => response.json())
                .then(data => {
                    all_characters.push(data[0])
                })
        }
        this.setState({characters: all_characters})
    }

    render() {
        let aux = []
        aux.push(<h2>Nombre: {this.props.value.title}</h2>)
        aux.push(<p>Temporada: {this.props.value.season}</p>)
        aux.push(<p>Episodio: {this.props.value.episode}</p>)
        aux.push(<p>Fecha de lanzamiento: {this.props.value.air_date}</p>)
        aux.push(<p>Personajes:</p>)
        for (let character of this.props.value.characters) {
            aux.push(<CharacterDetails key={character} name={character} data={this.state.characters} />)
        }
        return (
            <div>
                <div>{aux}</div>
            </div>
        )
    }

}

export default EpisodeDetail