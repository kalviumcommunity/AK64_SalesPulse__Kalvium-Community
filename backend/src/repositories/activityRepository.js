import { BaseRepository } from './baseRepository.js';

export class ActivityRepository extends BaseRepository {
  constructor() {
    super('activity');
  }
}

export default new ActivityRepository();
