import drugService from '../../services/drug';
import { ADD_DRUG } from '../mutation_types';

export const saveDrug = ({ commit, state }, drug) => {

    return drugService.save(drug)
        .then(data => {
            if (data.id) {
                commit(ADD_DRUG, data)
            }
            return data;

        })
}