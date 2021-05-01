import React from "react"

class CharacterDetails extends React.Component {

    constructor(props) {
        super(props)
        this.state = {}
        this.handleClick = this.handleClick.bind(this)
    }

    handleClick(event, character) {
        let aux = []
        try {
            Object.keys(this.props.data).forEach(async key => {
                let value = this.props.data[key];
                let aux2 = []
                if (character === value.name) {
                    aux.push(<h1>{value.name}</h1>)
                    aux.push(<img src={value.img} alt="Character's pic" height="250px"/>)
                    aux.push(<p>Sobrenombre: {value.nickname} </p>)
                    let works = ""
                    for (let work of value.occupation) {works = works + ", " + work}
                    aux.push(<p>Trabajos: {works}</p>)
                    aux.push(<p>Intérprete: {value.portrayed}</p>)
                    aux.push(<p>Estado: {value.state}</p>)
                    aux.push(<p>Temporadas en Breaking Bad: {value.appearance ? value.appearance.join(" - ") : null}</p>)
                    aux.push(<p>
                        Temporadas en Breaking Bad: {value.better_call_saul_appearance ? value.better_call_saul_appearance.join(" - ") : null}
                        </p>)

                    let string = "https://tarea-1-breaking-bad.herokuapp.com/api/quote?author=" + character.replace(/ /g, "+")
                    await fetch(string)
                        .then(response => response.json())
                        .then(data => aux2 = data)
                    aux.push(<p>Frases famosas: </p>)
                    for (let each of aux2) {
                        aux.push(<p>{each.quote}</p>)
                    }
                    this.setState({charToShow: aux})
                }
            })
        } catch(err) {
            aux.push(<h1>Mas lento por favor! La aplicación no ha terminado de hacer los fetch. Ahora, vuelve a presionar</h1>)
        }
        this.setState({charToShow: aux})
    }

    render() {
        return(
            <div>
                <div>
                    <button onClick={event => this.handleClick(event, this.props.name)}>
                        {this.props.name ? this.props.name : "Hubo error"}
                    </button>
                </div>
                <div>
                    {this.state.charToShow}
                </div>
            </div>
        )
    }

}

export default CharacterDetails