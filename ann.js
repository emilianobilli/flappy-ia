class ANN {

    constructor(id, topology) {
        this.topology = topology;
        this.id = id;
    }

    sigmoid(x) {  
        return 1 / (1 + Math.exp(-x));
    } 


    calculate(inputs) { 
        if (inputs.length != this.topology.inputs) {
            throw "Invalid number of inputs";
        }
        let i;
        let j;
        let k;
        let w;
        let value;
        let tmp;
        for (i=0; i<= this.topology.layers.length-1; i++) {
            tmp = new Array()
            for (j=0; j<= this.topology.layers[i].length-1; j++) {
                value = 0;
                for (k=0; k <= inputs.length-1; k++) {
                    w = this.topology.layers[i][j][k];
                    value = value + (inputs[k]*w);
                }
                if (this.topology.function == 'sigmoid') {
                    tmp.push(this.sigmoid(value));
                }
            }
            inputs = tmp;
        }
        if (inputs.length != this.topology.outputs_types.length) {
            throw "Invalid outputs";
        }
        console.log(inputs)
        for (i=0; i <= inputs.length-1; i++) {
            if (this.topology.outputs_types[i] == 'discrete') {
                if (inputs[i] < 0.5) {
                    inputs[i] = 0;
                } else {
                    inputs[i] = 1;
                }
            }
        }
        return inputs;
    }
}

/**
 * Example:
 * 
 * anns = new Array();
 * 
 * for (i = 0; i < population.length; i++) {
 *     // Init all ANN
 *     anns.push(new ANN(population[i].id, population[i].topology));
 * }
 * 
 * 
 */