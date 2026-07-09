import { BaseRepository } from './baseRepository.js';

export class UserRepository extends BaseRepository {
  constructor() {
    super('user');
  }

  // Domain-specific queries can be added here
}

export default new UserRepository();
