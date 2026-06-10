// Cross-feature primitive. Every slice that issues / verifies a token uses this.

import { importJWK, SignJWT, jwtVerify, JWTPayload, JWK } from 'jose';

export interface SigningKey {
  sign(payload: JWTPayload): Promise<string>;
  verify(token: string): Promise<JWTPayload>;
}

export class Ed25519SigningKey implements SigningKey {
  private constructor(
    private readonly privateKey: Awaited<ReturnType<typeof importJWK>>,
    private readonly publicKey: Awaited<ReturnType<typeof importJWK>>,
  ) {}

  static async fromJwk(privateJwk: JWK, publicJwk: JWK): Promise<Ed25519SigningKey> {
    const [priv, pub] = await Promise.all([
      importJWK(privateJwk, 'EdDSA'),
      importJWK(publicJwk, 'EdDSA'),
    ]);
    return new Ed25519SigningKey(priv, pub);
  }

  async sign(payload: JWTPayload): Promise<string> {
    return new SignJWT(payload).setProtectedHeader({ alg: 'EdDSA' }).sign(this.privateKey);
  }

  async verify(token: string): Promise<JWTPayload> {
    const { payload } = await jwtVerify(token, this.publicKey, { algorithms: ['EdDSA'] });
    return payload;
  }
}
