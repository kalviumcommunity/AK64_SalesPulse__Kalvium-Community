import { BaseRepository } from './baseRepository.js';

export class DealRepository extends BaseRepository {
  constructor() {
    super('deal');
  }
}

export default new DealRepository();
