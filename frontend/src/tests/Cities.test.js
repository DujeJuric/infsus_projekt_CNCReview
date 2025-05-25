import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Cities from '../components/CitiesLookup';


global.fetch = jest.fn(() =>
    Promise.resolve({
        ok: true,
        json: () => Promise.resolve(
            [
            { id: 1, naziv: "Zagreb" },
            { id: 2, naziv: "Split" },
            { id: 3, naziv: "Rijeka" }
            ]),
    })
);

jest.mock('../components/LookupContext', () => ({
    useLookup: () => ({
        cities: [
            { grad_id: 1, naziv: 'Zagreb' },
            { grad_id: 2, naziv: 'Split' }
        ],
        refreshLookup: jest.fn()
    })
}));

describe('Sifrarnik gradova', () => {
    beforeEach(() => {
        fetch.mockClear();
    });

    test('prikazuje gradove', () => {
        render(<Cities />);
        expect(screen.getByText('Zagreb')).toBeInTheDocument();
        expect(screen.getByText('Split')).toBeInTheDocument();
    });

    test('uređuje grad', async () => {
        render(<Cities />);
        fireEvent.click(screen.getAllByText('Uredi')[0]);
        const input = screen.getByDisplayValue('Zagreb');
        fireEvent.change(input, { target: { value: 'Osijek' } });

        fireEvent.click(screen.getByText('Spremi'));

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('/grad/editGrad/1'),
                expect.objectContaining({
                    method: 'POST',
                    body: JSON.stringify({ naziv: 'Osijek' }),
                })
            );
        });
    });

    test('onemogućava dodavanje duplikata', async () => {
        render(<Cities />);
        fireEvent.click(screen.getByText('Dodaj novi grad'));

        const input = screen.getByPlaceholderText('Naziv grada');
        fireEvent.change(input, { target: { value: 'Split' } });

        fireEvent.click(screen.getByText('Spremi'));

        expect(await screen.findByText('Već postoji grad s tim nazivom!')).toBeInTheDocument();
        expect(fetch).not.toHaveBeenCalled();
    });
});
