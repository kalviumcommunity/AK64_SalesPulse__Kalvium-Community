import { BaseRepository } from './baseRepository.js';

export class RecommendationRepository extends BaseRepository {
  constructor() {
    super('recommendation');
  }
}

export default new RecommendationRepository();
