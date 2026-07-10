import { BaseRepository } from './baseRepository.js';

export class EmailRepository extends BaseRepository {
  constructor() {
    super('email');
  }
}

export default new EmailRepository();
